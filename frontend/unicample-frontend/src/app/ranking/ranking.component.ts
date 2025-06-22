import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ranking',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ranking.component.html',
  styleUrl: './ranking.component.scss'
})
export class RankingComponent {
  @Output() closeModal = new EventEmitter<void>();

  // Puxar do banco de dados isso aqui
  players: string[] = [
    'Player 1: 1000 pts',
    'Player 2: 950 pts',
    'Player 3: 900 pts',
    'Player 4: 850 pts',
    'Player 5: 800 pts',
    'Player 6: 750 pts'
  ];

  onCloseButtonClick(): void {
    this.closeModal.emit();
  }
}