import {Component, Input, OnInit} from '@angular/core';
import {TurfListService} from '../services/turf-list.service';
import {TurfType} from '../models/turf.model';
import {UserService} from '../services/user.service';
import {IUser} from '../models/user.model';
import {IStatus} from '../models/api.model';
import {SnackBarService} from '../services/snackBar.service';
import {EasterEggService} from '../services/easter.service';

@Component({
    selector: 'app-turf-list',
    templateUrl: './turf-list.component.html',
    styleUrls: ['./turf-list.component.scss']
})
export class TurfListComponent implements OnInit {
    user: IUser = null;
    busy = false;
    turfUsers: IUser[] = [];

    @Input() miniView = false;

    constructor(private turfListService: TurfListService,
                private profileService: UserService,
                private snackBarService: SnackBarService,
                private easterEggService: EasterEggService) {
        this.profileService.getProfile().then(result => {
            this.user = result;
        });
        this.profileService.getActiveUsers().then(result => {
            this.turfUsers = result;
        });
    }

    ngOnInit() {
    }

    turfItem(turfType: TurfType = TurfType.BEER, amount = 1, turfUser = null) {
        if (!turfUser) {
            turfUser = this.user;
        }
        this.busy = true;
        this.turfListService.turfItem({
            turf_count: amount,
            turf_note: `${this.user.username} turved in BETA phase. Prev_amount${this.user.housemate.sum_bier}`,
            turf_type: turfType,
            turf_user_id: turfUser.id
        }).then(output => {
            if (output.status === IStatus.SUCCESS) {
                this.user.housemate = output.result;
                this.snackBarService.openSnackBar(
                    `Turved ${amount} ${turfType} on ${turfUser.housemate.id}. Total: ${this.user.housemate.sum_bier}`,
                    this.easterEggService.easterEggo());
            }
            this.busy = false;
        });
    }

}
