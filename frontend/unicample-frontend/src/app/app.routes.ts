import { Routes } from '@angular/router';
import { Home } from './features/home/home';
import { GameComponent } from './features/game/game.component';

export const routes: Routes = [
  { path: '', component:  Home},
  { path: 'game', component: GameComponent },
];
