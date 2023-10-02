import { Component, ViewEncapsulation, ElementRef, Input, OnInit, OnDestroy } from '@angular/core';
import { PopViewService } from '../_services';

@Component({
  selector: 'app-pop-view',
  templateUrl: './pop-view.component.html',
  styleUrls: ['./pop-view.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class PopViewComponent implements OnInit, OnDestroy {
  @Input() id?: string;
  isOpen = false;
  private element: any;

  constructor(private popviewService: PopViewService, private el: ElementRef) {
      this.element = el.nativeElement;
  }

  ngOnInit() {
    // add self (this modal instance) to the modal service so it can be opened from any component
    this.popviewService.add(this);

    // move element to bottom of page (just before </body>) so it can be displayed above everything else
    document.body.appendChild(this.element);

    // close modal on background click
    this.element.addEventListener('click', (el: any) => {
        if (el.target.className === 'app-pop-view') {
            this.close();
        }
    });
}
  ngOnDestroy() {
    // remove self from modal service
    this.popviewService.remove(this);

    // remove modal element from html
    this.element.remove();
}

open() {
    this.element.style.display = 'block';
    document.body.classList.add('app-pop-view-open');
    this.isOpen = true;
}

close() {
    this.element.style.display = 'none';
    document.body.classList.remove('app-pop-view-open');
    this.isOpen = false;
}
}
