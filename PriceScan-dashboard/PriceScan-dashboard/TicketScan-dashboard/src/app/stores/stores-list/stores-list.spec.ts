import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StoresList } from './stores-list';

describe('StoresList', () => {
  let component: StoresList;
  let fixture: ComponentFixture<StoresList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StoresList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StoresList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
