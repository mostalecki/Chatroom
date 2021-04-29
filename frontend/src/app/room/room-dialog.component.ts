import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'room-dialog',
  templateUrl: './room-dialog.component.html',
  styleUrls: ['./room-dialog.component.css'],
})
export class RoomDialogComponent implements OnInit {
  form: FormGroup;
  username: string;
  isPasswordProtected: boolean;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<RoomDialogComponent>,
    private router: Router
  ) {
    this.username = data.username;
    this.isPasswordProtected = data.isPasswordProtected;
    this.form = fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  ngOnInit() {}

  save() {
    this.dialogRef.close(this.form.value);
  }

  close() {
    this.dialogRef.close();
    this.router.navigateByUrl('/');
  }
}
