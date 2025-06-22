import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RankingService } from '../../core/services/rankingService';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-submit-score',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './submit-score.component.html',
  styleUrls: ['./submit-score.component.scss']
})
export class SubmitScoreComponent {
  @Input() pontuacao: number = 0;
  @Input() id_jogo: string = '';

  nomeJogador: string = '';

  constructor(private rankingService: RankingService) {}

  onSubmit(): void {
    console.log("Pontuação submetida!");
    this.rankingService.adicionaPontuacao(this.pontuacao, this.nomeJogador).subscribe({
      next: (response) => {
        console.log('Pontuação adicionada com sucesso:', response);
        window.location.href = '/';
      },
      error: (error) => {
        console.error('Erro ao adicionar pontuação:', error);
      }
    });
  }

  onIgnore(): void {
    window.location.href = '/';
  }

}
