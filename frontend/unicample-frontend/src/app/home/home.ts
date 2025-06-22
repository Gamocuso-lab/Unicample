import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RankingComponent } from '../ranking/ranking.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RankingComponent],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home implements OnInit, OnDestroy {

  images: string[] = [
    'assets/imagens/BCCL.jpg',
    'assets/imagens/BORA.jpg',
    'assets/imagens/CB1.jpg',
    'assets/imagens/CB2.jpg',
    'assets/imagens/FE.jpg',
    'assets/imagens/FEAGRI.jpg',
    'assets/imagens/FECAU.jpg',
    'assets/imagens/FEF.jpg',
    'assets/imagens/FEM.jpg',
    'assets/imagens/IA1.jpg',
    'assets/imagens/IB.jpg',
    'assets/imagens/IC1.jpg',
    'assets/imagens/IC2.jpg',
    'assets/imagens/IC3.jpg',
    'assets/imagens/IC4.jpg',
    'assets/imagens/IC5.jpg',
    'assets/imagens/IE1.jpg',
    'assets/imagens/IE2.jpg',
    'assets/imagens/IEL.jpg',
    'assets/imagens/IFCH1.jpg',
    'assets/imagens/IFCH2.jpg',
    'assets/imagens/IFGW1.jpg',
    'assets/imagens/IFGW3.jpg',
    'assets/imagens/IG.jpg',
    'assets/imagens/IMECC1.jpg',
    'assets/imagens/IMECC2.jpg',
    'assets/imagens/IQ.jpg',
    'assets/imagens/IQ2.jpg',
    'assets/imagens/PB1.jpg',
    'assets/imagens/PB2.jpg',
    'assets/imagens/PB3.jpg',
    'assets/imagens/PLASMA1.jpg',
    'assets/imagens/PLASMA2.jpg',
    'assets/imagens/Praça_do_CB.jpg',
    'assets/imagens/RU1.jpg',
    'assets/imagens/RU2.jpg',
  ];

  currentIndex: number = 0;
  private intervalId: any;
  private readonly INTERVAL_TIME_MS = 5000;

  showRankingModal: boolean = false;

  ngOnInit(): void {
    this.startCarousel();
  }

  ngOnDestroy(): void {
    this.stopCarousel();
  }

  startCarousel(): void {
    this.intervalId = setInterval(() => {
      this.nextImage();
    }, this.INTERVAL_TIME_MS);
  }

  stopCarousel(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  nextImage(): void {
    this.currentIndex = (this.currentIndex + 1) % this.images.length;
  }

  onPlayClick(): void {
    console.log('Botão "Jogar" clicado!');
  }

  onRankingClick(): void {
    this.showRankingModal = true;
  }

  onAboutUsClick(): void {
    console.log('Botão "Sobre nós" clicado!');
  }

  onCloseRankingModal(): void {
    this.showRankingModal = false;
  }
}