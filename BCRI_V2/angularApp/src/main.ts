/*
*  Protractor support is deprecated in Angular.
*  Protractor is used in this example for compatibility with Angular documentation tools.
*/
import { bootstrapApplication,provideProtractorTestingSupport } from '@angular/platform-browser';
import { FrontPageComponent } from './app/front-page/front-page.component';

bootstrapApplication(FrontPageComponent,
    {providers: [provideProtractorTestingSupport()]})
  .catch(err => console.error(err));
