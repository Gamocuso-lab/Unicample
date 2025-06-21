import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StreetViewService } from '../../core/services/streetviewService';

@Component({
  selector: 'app-street-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './street-view.component.html',
  styleUrl: './street-view.component.scss'
})
export class StreetViewComponent {
  @Input() id_jogo: string = '';

  constructor(private streetViewService: StreetViewService) { }

  ngOnInit() {
    if (!this.id_jogo) {
      console.error('id_jogo is not provided');
    }
    // Additional initialization logic can go here
    console.log(`StreetViewComponent initialized with id_jogo: ${this.id_jogo}`);
    // You can add logic to fetch and display the street view based on id_jogo
    // For example, you might want to call a service to get the street view data
    this.streetViewService.getJogoStreetView(this.id_jogo).subscribe(
      data => {
        document.getElementById('street-view-container')!.innerHTML = data;
      },
      error => {
        console.error('Error fetching street view data:', error);
      }
    );
  }

}
