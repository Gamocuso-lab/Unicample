import { Component, Input, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-notification',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.css'],
  animations: [
    trigger('notificationAnimation', [
      state('hidden', style({
        opacity: 0,
        transform: 'translateY(-30px)'
      })),
      state('visible', style({
        opacity: 1,
        transform: 'translateY(0)'
      })),
      transition('hidden => visible', [
        animate('300ms ease-out')
      ]),
      transition('visible => hidden', [
        animate('300ms ease-in')
      ])
    ])
  ]
})
export class NotificationComponent implements OnInit, OnDestroy {
  @Input() message: string = '';
  @Input() type: 'success' | 'error' | 'warning' | 'info' = 'info';
  @Input() duration: number = 5000; // Duração em ms

  animationState: 'visible' | 'hidden' = 'hidden';
  private timer: any;

  constructor(private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.show();
  }

  ngOnDestroy() {
    clearTimeout(this.timer);
  }

  private show() {
    setTimeout(() => {
      this.animationState = 'visible';
      this.cdr.detectChanges();

      this.timer = setTimeout(() => {
        this.animationState = 'hidden';
        this.cdr.detectChanges();

        setTimeout(() => {}, 300);
      }, this.duration);
    }, 0);
  }
}