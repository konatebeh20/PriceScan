import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StoresAchive } from './stores-achive';

describe('StoresAchive', () => {
  let component: StoresAchive;
  let fixture: ComponentFixture<StoresAchive>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StoresAchive]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StoresAchive);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
