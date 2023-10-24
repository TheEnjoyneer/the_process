import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FullRecapPageComponent } from './full-recap-page.component';

describe('FullRecapPageComponent', () => {
  let component: FullRecapPageComponent;
  let fixture: ComponentFixture<FullRecapPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FullRecapPageComponent]
    });
    fixture = TestBed.createComponent(FullRecapPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
