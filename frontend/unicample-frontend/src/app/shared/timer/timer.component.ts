import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-timer',
  imports: [CommonModule],
  templateUrl: './timer.component.html',
  styleUrl: './timer.component.scss'
})
export class TimerComponent {

  @Input() id_jogo: string = ''; // ID do jogo para identificar o timer
  @Input() tempoInicial: number | null = null; // Tempo inicial em segundos

  @Output() tempoAcabou =  new EventEmitter<void>()
  
  ngOnInit() {
    if (this.tempoInicial !== null && !localStorage.getItem(`game_timer_${this.id_jogo}`)) {
      this.startNewTimer(this.tempoInicial);
    } else {
      this.initializeTimer();
    }
  }

  ngOnDestroy() {
    this.stopTimer();
  }

  timeRemaining: number = 0; 
  timerInterval: any;
  
  startNewTimer(duration: number) {
    const expiryTime = Date.now() + (duration * 1000);

    console.log(`Iniciando novo timer para o jogo ${this.id_jogo} com duração de ${duration} segundos`);

    localStorage.setItem(`game_timer_${this.id_jogo}`, expiryTime.toString());

    this.initializeTimer();
  }
  
  initializeTimer() {
    const expiryTimeStr = localStorage.getItem(`game_timer_${this.id_jogo}`);

    if (!expiryTimeStr) {
      console.error('Não foi possível encontrar o timer do jogo');
      return;
    }
    
    const expiryTime = parseInt(expiryTimeStr, 10);
    const now = Date.now();
    
    if (expiryTime <= now) {
      this.tempoAcabou.emit();
      return;
    }
    
    this.timeRemaining = Math.floor((expiryTime - now) / 1000);
    
    this.timerInterval = setInterval(() => {
      this.timeRemaining -= 1;
      
      if (this.timeRemaining <= 0) {
        this.tempoAcabou.emit();
        this.stopTimer();
      }
    }, 1000);
  }
  
  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  get formattedTimeRemaining(): string {
    const minutes = Math.floor(this.timeRemaining / 60);
    const seconds = this.timeRemaining % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

}
