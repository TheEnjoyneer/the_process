import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FantasyBettingComponent } from './fantasy-betting.component';

describe('FantasyBettingComponent', () => {
  let component: FantasyBettingComponent;
  let fixture: ComponentFixture<FantasyBettingComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FantasyBettingComponent]
    });
    fixture = TestBed.createComponent(FantasyBettingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
