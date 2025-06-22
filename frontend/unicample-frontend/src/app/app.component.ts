import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Home } from './features/home/home';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,Home],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'unicample-frontend';
}