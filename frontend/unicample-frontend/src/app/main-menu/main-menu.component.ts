import { Component } from '@angular/core';
import { StreetViewComponent } from '../shared/street-view/street-view.component';

@Component({
  selector: 'app-main-menu',
  standalone: true,
  imports: [StreetViewComponent],
  templateUrl: './main-menu.component.html',
  styleUrl: './main-menu.component.scss'
})
export class MainMenuComponent {

}