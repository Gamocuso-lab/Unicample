import { Component } from '@angular/core';
import { StreetViewComponent } from '../../shared/street-view/street-view.component';
import { ImageViewerComponent } from '../../shared/image-viewer/image-viewer.component';
import { JogoService } from '../../core/services/jogoService';
import { GuessInputComponent } from '../../shared/guess-input/guess-input.component';
import { NotificationComponent } from '../../shared/notification/notification.component';
import { CommonModule } from '@angular/common';
import { TimerComponent } from '../../shared/timer/timer.component';
import { SubmitScoreComponent } from '../submit-score/submit-score.component';

@Component({
  selector: 'app-game',
  imports: [StreetViewComponent, ImageViewerComponent, GuessInputComponent, NotificationComponent, TimerComponent, SubmitScoreComponent, CommonModule],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss'
})
export class GameComponent {

  imageViewerPath: string = 'assets/imagens/CB1.jpg';
  id_jogo: number = 0;
  refreshCounter: number = 0;
  
  showNotification: boolean = false;
  typeNotification: 'success' | 'error' = 'success';
  messageNotification: string = '';

  tempoJogo: number | null = 0; // variável para armazenar o tempo do jogo
  score: number = 0; // variável para armazenar o score

  showSubmitScore: boolean = false; // variável para controlar a exibição do componente de submit score

  constructor(private jogoService: JogoService) {}

  ngOnInit() {
    const storedIdJogo = sessionStorage.getItem('id_jogo');
    
    if (!storedIdJogo) {
      console.log('Nenhum jogo encontrado na sessão. Criando novo jogo...');
      this.criarNovoJogo();
    } else {
      this.id_jogo = parseInt(storedIdJogo, 10);
      if (isNaN(this.id_jogo) || this.id_jogo <= 0) {
        console.error('ID do jogo inválido no sessionStorage. Criando novo jogo...');
        this.criarNovoJogo();
      } else {
        console.log('ID do jogo recuperado do sessionStorage:', this.id_jogo);
        this.carregaImagemApoio();
        this.carregaInformacoesJogo();
      }
    }
  }

  criarNovoJogo() {
    this.jogoService.criarJogo().subscribe({
      next: (response: any) => {
        this.id_jogo = response;
        sessionStorage.setItem('id_jogo', this.id_jogo.toString());
        console.log('Jogo criado com sucesso:', response);
        
        this.carregaInformacoesJogo();
        this.carregaImagemApoio();
          
      },
      error: (error) => {
        console.error('Erro ao criar jogo:', error);
      }
    });
  }


  finalizarJogoPorTempo() {
    
    this.jogoService.finalizaJogo(this.id_jogo).subscribe({
      next: (response) => {
        localStorage.removeItem(`game_timer_${this.id_jogo}`);
        sessionStorage.removeItem('id_jogo');
        console.log('Jogo finalizado por tempo:', response);
        this.showNotificationMessage('O tempo acabou!', 'error');

        setTimeout(() =>{
          this.showSubmitScore = true; 

        }, 4000)
      },
      error: (error) => {
        console.error('Erro ao finalizar jogo:', error);
      }
    });
  }

  carregaImagemApoio() {

    this.jogoService.getJogoImagem(this.id_jogo).subscribe({
      next: (response: any) => {
        this.imageViewerPath = response['imagem'];
        console.log('Imagem do jogo obtida com sucesso:', response);
      },
      error: (error) => {
        console.error('Erro ao obter imagem do jogo:', error);
      }
    });

  
  }

  carregaInformacoesJogo() {

    this.jogoService.getJogoInfo(this.id_jogo).subscribe({
      next: (response: any) => {
        this.tempoJogo = response['tempo'] || null;
        this.score = response['pontuacao'] || 0;
        console.log('Informações do jogo obtidas com sucesso:', response);
      },
      error: (error) => {
        console.error('Erro ao obter informações do jogo:', error);
      }
    });

  }

  atualizaScore() {

    this.jogoService.getJogoInfo(this.id_jogo).subscribe({
      next: (response: any) => {
        this.score = response['pontuacao'] || 0;
      },
      error: (error) => {
        console.error('Erro ao atualizar informações do jogo:', error);
      }
    });

  }

  onGuessSubmitted(guess: string) {
    this.jogoService.chute(this.id_jogo, guess).subscribe({
      next: (response: any) => {
        console.log('Chute enviado com sucesso:', response);

        if (!response) {
          this.showNotificationMessage("Você errou !", "error");
        } else {
          this.showNotificationMessage("Você acertou !", "success");
          this.atualizaScore();
        }

        this.refreshStreetView(); 
      },
      error: (error) => {
        console.error('Erro ao enviar chute:', error);                                         
      }
    });
  }

  refreshStreetView() {
    this.refreshCounter++; // Incrementar este valor causará o refresh
    this.carregaImagemApoio();
  }

  showNotificationMessage(message: string, type: 'success' | 'error') {
    this.showNotification = true;
    this.typeNotification = type;
    this.messageNotification = message;
    setTimeout(() => {
      this.showNotification = false;
    }, 5300); 
  }

}
