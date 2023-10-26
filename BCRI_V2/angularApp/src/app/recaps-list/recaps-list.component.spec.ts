import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecapsListComponent } from './recaps-list.component';

describe('RecapsListComponent', () => {
  let component: RecapsListComponent;
  let fixture: ComponentFixture<RecapsListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RecapsListComponent]
    });
    fixture = TestBed.createComponent(RecapsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
