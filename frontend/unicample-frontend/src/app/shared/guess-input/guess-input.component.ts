import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-guess-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './guess-input.component.html',
  styleUrls: ['./guess-input.component.scss']
})

export class GuessInputComponent implements OnInit {

  @Output() guessSubmitted = new EventEmitter<string>();

  isPanelOpen = false;
  selectedValue: string | null = null;
  filterText: string = '';

  //puxar do banco de dados
  private allLocations: string[] = [
    "Instituto de Física Gleb Wataghin",
    "Praça Do Ciclo Básico",
    "Biblioteca Cesar Lattes",
    "Ciclo Básico I",
    "Ciclo Básico II",
    "Biblioteca de Obras Raras",
    "Faculdade de Educação",
    "Faculdade de Engenharia Agrícola",
    "Faculdade de Engenharia Civil Arquitetura e Urbanismo",
    "Faculdade de Educação Física",
    "Faculdade de Engenharia Mecânica",
    "Instituto de Artes",
    "Instituto da Biologia",
    "Instituto da Computação",
    "Instituto da Economia",
    "Instituto de Estudo Da Linguagem",
    "Instituto de Filosofia e Ciências Humanas",
    "Instituto de Geociências",
    "Instituto de Matemática Estatística e Computação Científica",
    "Instituto de Quimica",
    "Plasma",
    "Restaurante Universitário"
  ];

  filteredLocations: string[] = [];

  ngOnInit(): void {
    this.filteredLocations = [...this.allLocations];
  }

  openPanel(): void {
    this.isPanelOpen = true;
  }

  closePanel(): void {
    this.isPanelOpen = false;
  }

  selectLocation(location: string): void {
    this.selectedValue = location;
    this.filterLocations();
  }

  submitGuess(): void {
    if (this.selectedValue) {
      this.guessSubmitted.emit(this.selectedValue);
      this.closePanel();
    } else {
      alert("Por favor, selecione um local da lista.");
    }
  }

  filterLocations(): void {
    const text = this.filterText.toLowerCase();
    this.filteredLocations = this.allLocations.filter(location =>
      location.toLowerCase().includes(text)
    );
  }
}