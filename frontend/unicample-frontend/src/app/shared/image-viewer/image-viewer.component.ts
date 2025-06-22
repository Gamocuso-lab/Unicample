import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-image-viewer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './image-viewer.component.html',
  styleUrl: './image-viewer.component.scss',
  animations: [
    trigger('slideInOut', [
      state('closed', style({
        transform: 'translateX(calc(-100% + 32px))',  // Deixa apenas o botão visível
      })),
      state('open', style({
        transform: 'translateX(0)',
      })),
      transition('closed => open', animate('300ms ease-in')),
      transition('open => closed', animate('300ms ease-out'))
    ])
  ]
})
export class ImageViewerComponent {
  @Input() path_imagem: string = '';
  @Input() blur: number = 4 ;
  isOpen = false;

  togglePanel() {
    this.isOpen = !this.isOpen;
  }
}