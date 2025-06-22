import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../enviroment';

@Injectable({
    providedIn: 'root'
})

export class LocaisService {

    apiUrl: string = "";

    constructor(private http: HttpClient) {
        this.apiUrl = `${environment.apiUrl}/dados`;
    }

    public getLocais() {
        try {
            return this.http.get(`${this.apiUrl}/get-locais`);
        } catch (error) {
            console.error('Erro ao obter locais:', error);
            throw error;
        }
    }

}