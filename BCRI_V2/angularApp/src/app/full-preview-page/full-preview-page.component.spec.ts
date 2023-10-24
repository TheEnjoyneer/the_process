import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FullPreviewPageComponent } from './full-preview-page.component';

describe('FullPreviewPageComponent', () => {
  let component: FullPreviewPageComponent;
  let fixture: ComponentFixture<FullPreviewPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FullPreviewPageComponent]
    });
    fixture = TestBed.createComponent(FullPreviewPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
