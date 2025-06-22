import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LocaisService } from '../../core/services/locaisService';

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
  private allLocations: any[] = [
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

  filteredLocations: any[] = [];

  constructor(private locaisService: LocaisService) {}

  ngOnInit(): void {
    this.locaisService.getLocais().subscribe({
      next: (response: any) => {
        this.allLocations = response;
        this.filteredLocations = [...this.allLocations.map((loc: any) => loc.nome)];
      },
      error: (error) => {
        console.error('Erro ao obter locais:', error);
      }
    });
  }

  openPanel(): void {
    this.isPanelOpen = true;
    document.getElementById('filterInput')?.focus(); 
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
      this.selectedValue = null; // Limpa a seleção após o envio
      this.filterText = ''; // Limpa o filtro de texto
      this.filterLocations();
      this.closePanel();
    } else {
      alert("Por favor, selecione um local da lista.");
    }
  }

  filterLocations(): void {
    const text = this.filterText.toLowerCase();
    this.filteredLocations = this.allLocations.filter(location =>
      location.nome.toLowerCase().includes(text)
    ).map(location => location.nome);
  }
}