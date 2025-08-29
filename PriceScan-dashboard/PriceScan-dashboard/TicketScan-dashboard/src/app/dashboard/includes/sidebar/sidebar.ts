import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss']
})
export class SidebarComponent {
  @Input() isSidebarCollapsed: boolean = false;
  @Input() currentPage: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile' = 'dashboard';
  @Output() sidebarToggle = new EventEmitter<void>();
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile'>();

  toggleSidebar() {
    this.sidebarToggle.emit();
  }

  showPage(page: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile') {
    this.pageChange.emit(page);
  }
}
