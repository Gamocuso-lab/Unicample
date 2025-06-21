import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../enviroment';

@Injectable({
  providedIn: 'root'
})
export class StreetViewService {

    apiUrl = "";

    constructor(private http: HttpClient) { 

        this.apiUrl = environment.apiUrl;

    }

    getJogoStreetView(id_jogo: string) {

        return this.http.get(`${this.apiUrl}/jogo/${id_jogo}/streetview`, { responseType: 'text' });

    }

}