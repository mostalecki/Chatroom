import { Injectable } from '@angular/core';


@Injectable()
export class JwtService {

  getToken(): string {
    return window.localStorage['jwtToken'];
  }

  saveToken(token: String) {
    window.localStorage['jwtToken'] = token;
  }

  getRefreshToken(): string {
    return window.localStorage['jwtRefreshToken'];
  }

  saveRefreshToken(token: string) {
    window.localStorage['jwtRefreshToken'] = token;
  }

  destroyToken() {
    window.localStorage.removeItem('jwtToken');
  }

}
