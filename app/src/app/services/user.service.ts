import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {IUser} from '../models/user.model';
import {AuthService} from './auth.service';
import {FormGroup} from '@angular/forms';

@Injectable({
    providedIn: 'root'
})
export class UserService {

    API_URL: string = environment.baseUrl;

    constructor(private httpClient: HttpClient, private auth: AuthService) {
    }

    checkHouse(user: number = this.auth.getTokenClaims().user_id) {
        return user === 2;
    }

    getHouseProfile(user: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (user === 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/house/${user.toString()}/`, {}).toPromise();
        }
        return Promise.resolve(null);
    }

    // Jwt-claim based profile getter (guaranteed by guard)
    getProfile(user: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (user !== 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user/${user.toString()}/`, {}).toPromise();
        }
        return Promise.resolve(null);
    }

    getFullProfile(user: number = this.auth.getTokenClaims().user_id): Promise<IUser> {
        if (user !== 2) {
            return this.httpClient.get<IUser>(`${this.API_URL}/user-full/${user.toString()}/`, {})
                .toPromise();
        }
        return Promise.resolve(null);
    }

    getActiveUsers(): Promise<IUser[]> {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/`, {})
            .toPromise();
    }

    // Jwt-claim based user-id getter (guaranteed by guard)
    getUserId(): number {
        return this.auth.getTokenClaims().user_id;
    }

    checkUsername(username: string) {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?username__iexact=${username}`);
    }

    checkEmail(email: string) {
        return this.httpClient.get<IUser[]>(`${this.API_URL}/user/?email__iexact=${email}`);
    }

    createOrUpdate(userForm: FormGroup) {
        return this.httpClient.post<IUser>(`${this.API_URL}/user-full/`, userForm.value).toPromise();
    }
}
