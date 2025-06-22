import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-submit-score',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './submit-score.component.html',
  styleUrls: ['./submit-score.component.scss']
})
export class SubmitScoreComponent {



  onSubmit(): void {
    console.log("Pontuação submetida!");
  }


  onIgnore(): void {
    console.log("Ação ignorada.");
  }

}
