import {Component, OnInit} from '@angular/core';
import {IAttachments} from '../../../models/attachments.model';
import {IReceipt, IReceiptCost, SHARE} from '../../../models/receipt.model';
import {ReceiptService} from '../../../services/receipt.service';
import {FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {FileValidator} from 'ngx-material-file-input';
import {UserService} from '../../../services/user.service';
import {IUser} from '../../../models/user.model';
import {ThesauService} from '../../../services/thesau.service';
import {SnackBarService} from '../../../services/snackBar.service';

interface IReceiptCostUser extends IReceiptCost {
    user?: IUser;
}

@Component({
    selector: 'app-upload-receipt',
    templateUrl: './upload-receipt.component.html',
    styleUrls: ['./upload-receipt.component.scss']
})
export class UploadReceiptComponent implements OnInit {
    readonly maxAttachmentSize = 50 * 2 ** 20;

    SHARE = SHARE;

    loadingUsers = true;
    user: IUser;
    isThesau = true;
    allUsers: IUser[];
    billableUsers: IUser[];
    billedUsers: IReceiptCostUser[] = [];

    uploadReceiptForm = new FormGroup({
        show_old_housemates: new FormControl(false),
        receipt_title: new FormControl('',
            {
                validators: [Validators.maxLength(100), Validators.required],
            }),
        receipt_description: new FormControl('',
            {
                validators: [Validators.maxLength(300)],
            }),
        receipt_cost: new FormControl(0,
            {
                validators: [Validators.required],
            },
        ),
        charged_user: new FormControl(null),
        reimbursed_user: new FormControl(null, {
            validators: [Validators.required]
        }),
        share_cost_method: new FormControl({value: 'share_all', disabled: true}),
        attachment: new FormControl(null,
            {
                validators: [Validators.required, FileValidator.maxContentSize(this.maxAttachmentSize)]
            })
    });

    constructor(
        private receiptService: ReceiptService,
        private userService: UserService,
        private thesauService: ThesauService,
        private snackBar: SnackBarService) {
    }

    ngOnInit() {
        this.uploadReceiptForm.disable();

        const showOldHousemates = this.C('show_old_housemates');
        this.userService.getProfile().then(response => {
            this.user = response;
            this.isThesau = !!this.userService.findThesauGroup(this.user.groups);
            this.uploadReceiptForm.enable();
            this.C('share_cost_method').disable();
            this.thesauService.getBillableUsers().then(output => {
                this.billableUsers = output.result;
            });
            this.thesauService.getAllUsers(showOldHousemates.value).then(output => {
                this.allUsers = output;
                this.uploadReceiptForm.enable();
                this.loadingUsers = false;

                if (this.isThesau) {
                    showOldHousemates.valueChanges.subscribe(change => {
                        this.updateUserDropdown(change);
                    });
                    this.C('charged_user').valueChanges.subscribe(result => {
                        this.addBillableUser(result);
                    });
                    this.C('share_cost_method').valueChanges.subscribe(result => {
                        if (result === SHARE.ALL || result === SHARE.HOUSE) {
                            this.C('charged_user').disable();
                        } else {
                            this.C('charged_user').enable();
                        }
                        console.log(this.getFormValidationErrors());
                    });
                } else {
                    this.C('show_old_housemates').disable();
                    this.C('share_cost_method').disable();
                    this.C('reimbursed_user').disable();
                    this.C('charged_user').disable();
                }
            }, error => {
                if ('error' in error) {
                    this.snackBar.openSnackBar('Error: ' + error.error, 'Ok');
                } else {
                    this.snackBar.openSnackBar('An unknown error happened. ' + error, 'Ok');
                }
            });
        });
    }

    getFormValidationErrors() {
        Object.keys(this.uploadReceiptForm.controls).forEach(key => {
            const controlErrors: ValidationErrors = this.uploadReceiptForm.get(key).errors;
            if (controlErrors != null) {
                Object.keys(controlErrors).forEach(keyError => {
                    console.log('Key control: ' + key + ', keyError: ' + keyError + ', err value: ', controlErrors[keyError]);
                });
            }
        });
    }

    updateUserDropdown(change: boolean) {
        if (this.isThesau) {
            this.loadingUsers = true;
            this.thesauService.getAllUsers(change).then(output => {
                this.allUsers = output;
                this.loadingUsers = false;
            });
        }
    }

    addBillableUsers(popup = false) {
        if (this.billableUsers || !this.loadingUsers) {
            let addedUserCount = 0;
            this.billableUsers.forEach(user => {
                if (!this.billedUsers.find(bu => bu.affected_user_id === user.id)) {
                    this.billedUsers.push({
                        user,
                        affected_user_id: user.id,
                        cost_user: 0.00
                    });
                    addedUserCount++;
                }
            });
            if (popup) {
                if (addedUserCount) {
                    this.snackBar.openSnackBar('Added ' + addedUserCount.toString() + ' users to receipt', 'Thx');
                } else {
                    this.snackBar.openSnackBar('No missing users', 'Nice');
                }
            }
        } else if (popup) {
            this.snackBar.openSnackBar('It seems users are still loading, report bug if incorrect.', 'Okay.');
        }
    }

    splitCost(popup = true) {
        const cost = this.V('receipt_cost');
        if (cost && this.billedUsers && this.billedUsers.length) {
            const split = this.V('receipt_cost') / this.billedUsers.length;
            this.billedUsers.forEach(bu => bu.cost_user = split);
            this.snackBar.openSnackBar(
                'Split ' + this.V('receipt_cost').toString(), 'Thx');
        } else if (popup) {
            if (!cost) {
                this.snackBar.openSnackBar('No cost set.', 'Whoops');
            } else {
                this.snackBar.openSnackBar('No users added.', 'Whoops');
            }
        }
    }

    emptyBilledUsers() {
        this.billedUsers = [];
    }

    deleteBilledUser(index) {
        this.billedUsers.splice(index, 1);
    }

    addBillableUser(user: IUser) {
        if (user) {
            this.billedUsers.push({
                user,
                affected_user_id: user.id,
                cost_user: 0.00
            });
        }
    }

    processForm() {
        const formData = this.uploadReceiptForm.value;
        const costMethod = formData.share_cost_method as SHARE;
        const reimbursedUser = formData.reimbursed_user;
        const removeKeys = ['reimbursed_user', 'share_cost_method', 'show_old_housemates', 'attachment', 'charged_user'];
        removeKeys.forEach(key => {
            if (key in formData) {
                delete formData[key];
            }
        });

        const newReceipt: IReceipt = formData;
        newReceipt.receipt_costs_split = [];
        newReceipt.receipt_costs_split.push({
            cost_user: -formData.receipt_cost,
            affected_user_id: reimbursedUser ? reimbursedUser.id : this.user.id
        });
        if (costMethod === SHARE.ALL) {
            this.emptyBilledUsers();
            this.addBillableUsers(false);
            this.splitCost(false);
        } else if (costMethod === SHARE.HOUSE) {
            this.billedUsers = [{
                affected_user_id: 2,
                cost_user: formData.receipt_cost,
            }];
            this.splitCost(false);
        } else {
            this.billedUsers = [{
                affected_user_id: 2,
                cost_user: formData.receipt_cost,
            }];
            this.splitCost(false);
        }

        this.billedUsers.forEach(receiptCost => {
            newReceipt.receipt_costs_split.push({
                cost_user: receiptCost.cost_user,
                affected_user_id: receiptCost.affected_user_id
            });
        });
        if (!newReceipt.receipt_description) {
            newReceipt.receipt_description = '';
        }
        return newReceipt;
    }

    submitReceipt() {
        this.C('charged_user').disable();
        if (this.uploadReceiptForm.valid) {
            const receipt = this.processForm();
            const attachments = this.V('attachment')._files;
            const upload: IAttachments<IReceipt> = {
                attachments,
                json_object: receipt,
            };
            this.receiptService.uploadReceipt(upload).then(
                data => {
                    this.uploadReceiptForm.reset();
                    this.snackBar.openSnackBar('Receipt uploaded successfully!', 'Nice');
                },
                error => {
                    if ('error' in error && 'message' in error.error) {
                        this.snackBar.openSnackBar('Error from server: ' + error.error.message, 'Aight');
                    } else if ('error' in error) {
                        this.snackBar.openSnackBar('Unknown error: ' + error.error, 'Okay');
                    } else {
                        this.snackBar.openSnackBar('Unknown error: ' + error, 'Okay');
                        console.log(error);
                    }
                }
            );
        } else {
            this.uploadReceiptForm.markAllAsTouched();
        }
        this.C('charged_user').enable();
    }

    public V(control: string) {
        return this.uploadReceiptForm.get(control).value;
    }

    public E(control: string) {
        return this.uploadReceiptForm.controls[control].errors;
    }

    public C(control: string) {
        return this.uploadReceiptForm.controls[control];
    }

}
