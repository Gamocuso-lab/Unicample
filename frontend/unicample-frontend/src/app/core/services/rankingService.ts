import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../enviroment';

@Injectable({
  providedIn: 'root'
})
export class RankingService {
  private apiUrl = "";

  constructor(private http: HttpClient) {
    this.apiUrl = `${environment.apiUrl}/ranking`;
  }

  public getRanking() {
    try {
      return this.http.get(`${this.apiUrl}`);
    } catch (error) {
      console.error('Erro ao obter ranking:', error);
      throw error;
    }
  }

public adicionaPontuacao(pontuacao: number, nome: string) {
    try {
        return this.http.post(`${this.apiUrl}/adicionar`, { nome, pontuacao });
    } catch (error) {
        console.error('Erro ao adicionar pontuação ao ranking:', error);
        throw error;
    }
}
}