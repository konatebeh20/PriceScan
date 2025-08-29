import { TestBed } from '@angular/core/testing';

import { Price } from './price';

describe('Price', () => {
  let service: Price;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Price);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
