import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StoresDetails } from './stores-details';

describe('StoresDetails', () => {
  let component: StoresDetails;
  let fixture: ComponentFixture<StoresDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StoresDetails]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StoresDetails);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
