import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmitScoreComponent } from './submit-score.component';

describe('SubmitScoreComponent', () => {
  let component: SubmitScoreComponent;
  let fixture: ComponentFixture<SubmitScoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubmitScoreComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubmitScoreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
