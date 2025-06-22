import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-about-us',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './about-us.component.html',
  styleUrl: './about-us.component.scss'
})
export class AboutUsComponent {
  @Output() closeModal = new EventEmitter<void>();

  title: string = 'Sobre Nós';
  paragraphs: string[] = [
    'Este é o projeto final da disciplina MC322, Programação Orientada a Objetos.',
    'Somos um grupo de 3 alunos da Unicamp e este jogo foi inspirado no jogo Geoguessr, porém nos domínios da Unicamp.',
    'Colaboradores:',
    'Gabriel Moreira Cunha de Souza',
    'Breno Moura Pires de Oliveira',
    'João Vítor Albuquerque Mafra'
  ];

  onCloseButtonClick(): void {
    this.closeModal.emit();
  }
}