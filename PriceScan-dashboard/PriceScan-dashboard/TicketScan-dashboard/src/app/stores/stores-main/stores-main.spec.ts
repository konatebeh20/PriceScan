import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StoresMain } from './stores-main';

describe('StoresMain', () => {
  let component: StoresMain;
  let fixture: ComponentFixture<StoresMain>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StoresMain]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StoresMain);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
