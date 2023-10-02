import { TestBed } from '@angular/core/testing';

import { FlaskDataService } from './flask-data.service';

describe('FlaskDataService', () => {
  let service: FlaskDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FlaskDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
