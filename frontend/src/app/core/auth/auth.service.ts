import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

import { LoginResponse } from '../models/gene.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  private readonly tokenKey =
    'genomic-data-platform-admin-token';

  login(
    username: string,
    password: string,
  ): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(
        '/api/v1/auth/login',
        {
          username,
          password,
        },
      )
      .pipe(
        tap((response) => {
          sessionStorage.setItem(
            this.tokenKey,
            response.accessToken,
          );
        }),
      );
  }

  logout(): void {
    sessionStorage.removeItem(this.tokenKey);
    void this.router.navigateByUrl('/');
  }

  getToken(): string | null {
    return sessionStorage.getItem(this.tokenKey);
  }

  isAuthenticated(): boolean {
    const token = this.getToken();

    if (!token) {
      return false;
    }

    try {
      const parts = token.split('.');

      if (parts.length !== 3) {
        this.clearInvalidToken();
        return false;
      }

      const normalized = parts[1]
        .replace(/-/g, '+')
        .replace(/_/g, '/');

      const padded = normalized.padEnd(
        Math.ceil(normalized.length / 4) * 4,
        '=',
      );

      const payload = JSON.parse(
        atob(padded),
      ) as {
        exp?: number;
      };

      if (
        typeof payload.exp !== 'number' ||
        payload.exp * 1000 <= Date.now()
      ) {
        this.clearInvalidToken();
        return false;
      }

      return true;
    } catch {
      this.clearInvalidToken();
      return false;
    }
  }

  private clearInvalidToken(): void {
    sessionStorage.removeItem(this.tokenKey);
  }
}
