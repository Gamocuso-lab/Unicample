import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../enviroment';

@Injectable({
  providedIn: 'root'
})
export class JogoService {
  private apiUrl = "";

  constructor(private http: HttpClient) {
    this.apiUrl = `${environment.apiUrl}/jogo`;
  }

public criarJogo() {
    try {
        return this.http.post(`${this.apiUrl}/create`, {});
    } catch (error) {
        console.error('Erro ao criar jogo:', error);
        throw error;
    }
  }

  public getJogoInfo(id_jogo: number) {
    try {
        return this.http.get(`${this.apiUrl}/infos?jogo_id=${id_jogo}`);
    } catch (error) {
        console.error('Erro ao obter informações do jogo:', error);
        throw error;
    }
  }

  public getJogoImagem(id_jogo: number) {
    try {
        return this.http.get(`${this.apiUrl}/imagem?id_jogo=${id_jogo}`);
    } catch (error) {
        console.error('Erro ao obter imagem do jogo:', error);
        throw error;
    }
  }

  public chute(id_jogo: number, chute: string) {

    try {
        return this.http.get(`${this.apiUrl}/chute?id_jogo=${id_jogo}&local=${chute}`);
    } catch (error) {
        console.error('Erro ao enviar chute:', error);
        throw error;
    }
  }

}
