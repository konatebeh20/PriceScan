import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StoresFavorie } from './stores-favorie';

describe('StoresFavorie', () => {
  let component: StoresFavorie;
  let fixture: ComponentFixture<StoresFavorie>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StoresFavorie]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StoresFavorie);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
