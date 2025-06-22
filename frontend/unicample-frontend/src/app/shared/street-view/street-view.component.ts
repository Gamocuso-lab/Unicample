import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-street-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './street-view.component.html',
  styleUrl: './street-view.component.scss'
})
export class StreetViewComponent {
  @Input() id_jogo: string = '';
  safeUrl: SafeResourceUrl = '';

  @Input() refreshTrigger: number = 0;

  constructor(
    private sanitizer: DomSanitizer
  ) { }

  ngOnInit() {
    this.loadIframe();
  }
  
  ngOnChanges() {
    // Se refreshTrigger ou id_jogo mudar, recarrega o iframe
    this.loadIframe();
  }
  
  loadIframe() {
    if (!this.id_jogo) {
      console.error('id_jogo is not provided');
    } else {
      this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
        `http://localhost:8000/jogo/${this.id_jogo}/streetview?v=${Date.now()}`
      );
    }
  }
  
  // Método público para forçar o refresh
  refresh() {
    this.loadIframe();
  }

}
