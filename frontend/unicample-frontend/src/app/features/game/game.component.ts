import { Component } from '@angular/core';
import { StreetViewComponent } from '../../shared/street-view/street-view.component';
import { ImageViewerComponent } from '../../shared/image-viewer/image-viewer.component';
import { JogoService } from '../../core/services/jogoService';
import { GuessInputComponent } from '../../shared/guess-input/guess-input.component';

@Component({
  selector: 'app-game',
  imports: [StreetViewComponent, ImageViewerComponent, GuessInputComponent],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss'
})
export class GameComponent {

  imageViewerPath: string = 'assets/imagens/CB1.jpg';
  id_jogo: number = 0;
  refreshCounter: number = 0;

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
        
        // Carrega informações somente depois de criar o jogo com sucesso
        this.carregaInformacoesJogo();
      },
      error: (error) => {
        console.error('Erro ao criar jogo:', error);
      }
    });
  }

  carregaInformacoesJogo() {

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

  onGuessSubmitted(guess: string) {
    this.jogoService.chute(this.id_jogo, guess).subscribe({
      next: (response: any) => {
        console.log('Chute enviado com sucesso:', response);

        this.refreshStreetView(); 
      },
      error: (error) => {
        console.error('Erro ao enviar chute:', error);                                         
      }
    });
  }

  refreshStreetView() {
    this.refreshCounter++; // Incrementar este valor causará o refresh
    this.carregaInformacoesJogo();
  }

}
