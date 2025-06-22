import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RankingService } from '../../core/services/rankingService';

@Component({
  selector: 'app-ranking',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ranking.component.html',
  styleUrl: './ranking.component.scss'
})
export class RankingComponent {
  @Output() closeModal = new EventEmitter<void>();

  players: any[] = [];

  constructor(private rankingService: RankingService) {}

  ngOnInit() {
    this.carregarRanking();
  }

  carregarRanking() {
    this.rankingService.getRanking().subscribe({
      next: (response: any) => {
        this.players = response || [];
      },
      error: (error) => {
        console.error('Erro ao obter ranking:', error);
      }
    });
  }

  onCloseButtonClick(): void {
    this.closeModal.emit();
  }
}