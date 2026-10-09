import {
  Component,
  inject,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  Router,
  RouterLink,
} from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-admin-login',
  imports: [
    FormsModule,
    RouterLink,
  ],
  templateUrl: './admin-login.html',
  styleUrl: './admin-login.scss',
})
export class AdminLoginPage {
  private readonly auth =
    inject(AuthService);

  private readonly router =
    inject(Router);

  readonly loading = signal(false);
  readonly error = signal('');

  username = 'admin';
  password = '';

  submit(): void {
    if (
      !this.username.trim() ||
      !this.password
    ) {
      this.error.set(
        'Enter both username and password.',
      );
      return;
    }

    this.loading.set(true);
    this.error.set('');

    this.auth
      .login(
        this.username.trim(),
        this.password,
      )
      .subscribe({
        next: () => {
          this.password = '';
          this.loading.set(false);

          void this.router.navigateByUrl(
            '/admin',
          );
        },
        error: () => {
          this.password = '';
          this.loading.set(false);
          this.error.set(
            'Invalid administrator credentials.',
          );
        },
      });
  }
}
