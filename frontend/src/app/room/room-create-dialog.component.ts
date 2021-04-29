import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Room } from 'app/core';

@Component({
  selector: 'room-create-dialog',
  templateUrl: './room-create-dialog.component.html',
  styleUrls: ['./room-dialog.component.css'],
})
export class RoomCreateDialogComponent implements OnInit {
  form: FormGroup;
  name: string;
  isPrivate: boolean;
  password: string;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<RoomCreateDialogComponent>
  ) {
    this.form = fb.group({
      name: [
        '',
        Validators.compose([Validators.minLength(5), Validators.required]),
      ],
      isPrivate: [false, Validators.required],
      password: ['', Validators.minLength(5)],
    });
  }

  ngOnInit() {}

  save() {
    this.dialogRef.close(this.form.value);
  }

  close() {
    this.dialogRef.close();
  }
}
