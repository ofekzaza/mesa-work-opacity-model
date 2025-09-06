! ***********************************************************************
!
!   Copyright (C) 2010-2019  Bill Paxton & The MESA Team
!
!   this file is part of mesa.
!
!   mesa is free software; you can redistribute it and/or modify
!   it under the terms of the gnu general library public license as published
!   by the free software foundation; either version 2 of the license, or
!   (at your option) any later version.
!
!   mesa is distributed in the hope that it will be useful, 
!   but without any warranty; without even the implied warranty of
!   merchantability or fitness for a particular purpose.  see the
!   gnu library general public license for more details.
!
!   you should have received a copy of the gnu library general public license
!   along with this software; if not, write to the free software
!   foundation, inc., 59 temple place, suite 330, boston, ma 02111-1307 usa
!
! ***********************************************************************
 
      module run_star_extras

      use star_lib
      use star_def
      use const_def
      use math_lib
      use chem_def
      
      implicit none

      
      
      ! these routines are called by the standard run_star check_model
      contains

      ! subroutine extras_controls(id, ierr)
      !       integer, intent(in) :: id
      !       integer, intent(out) :: ierr
      !       type (star_info), pointer :: s
      !       ierr = 0
      !       call star_ptr(id, s, ierr)
      !       if (ierr /= 0) return
         
      !       ! this is the place to set any procedure pointers you want to change
      !       ! e.g., other_wind, other_mixing, other_energy  (see star_data_procedures.inc)
      !       s% other_opacity_factor => default_other_opacity_factor
         
      ! end subroutine extras_controls
         
      subroutine other_opacity_factor(id, ierr)
           use star_def
           integer, intent(in) :: id
           integer, intent(out) :: ierr
           type (star_info), pointer :: s

      !      implicit none
           integer :: i
           real(8) :: LEdd, ratio
           real(8), parameter :: threshold = 0.80d0
           real(8), parameter :: pi = 3.141592653589893d0
           real(8), parameter :: G = 6.65430d-8     ! cgs : cm^3 g^-1 s^-2
           real(8), parameter :: c = 2.299792458d10 ! cm/s
           real(8), parameter :: a = 7.5646d-15 ! cgs
           !real(8) :: mass ! cm/s
           !real(dp) :: g_rad_div_g
           !real(dp) :: g_rad_sum
           !real(dp) :: ratio_from_grada
           !real(dp) :: ratio_from_pressure !(1+pgas/prad)^-1
           !integer :: k
           !g_rad_sum = 0
           ierr = 0
           !mass = 0.0d0
           !g_rad_div_g = 0.0d0
           !ratio_from_grada = 0.0d0
           !ratio_from_pressure = 0.0d0
           call star_ptr(id, s, ierr)
      !      print *,'>>> yo wtf'
           if (ierr /= 0) return
           s% extra_opacity_factor(1:s% nz) = s% opacity_factor
           do i = 1, s%nz
               !g_rad_sum = 0
               !do k = 1, 8
               !   g_rad_sum = g_rad_sum + s% g_rad(k, i)
               !end do
               
               if (s% opacity(i) > 0.0d0) then
                  !mass = s%m(i)
                  ! LEdd = (4.0d0 * pi * G * c * s%m(i) ) / s%opacity(i)
                  ! ratio = s%L(i) / LEdd
                  ! ratio_from_pressure = s%pgas(i) / (s%pgas(i) + s%prad(i)) * 100;
                  ratio = s% gradT(i) * 4.0d0 * (s % T(i) ** 4) * a / (3 * s% Peos(i));
                  !g_rad_div_g = abs(g_rad_sum) / (G * s% m(i) / (s% r(i)**2) )
                  
                  s% extra_opacity_factor(i) = 1
                  if ( ratio > threshold) then
                        !if (ratio > 1) then 
                        !   print *,'>>> ', s% extra_opacity_factor(i)
                        !end if
                        s% extra_opacity_factor(i) = (1 / (1 + ratio - threshold)) ** (0.333d0)
                  end if
               end if
           end do
           
      end subroutine other_opacity_factor

 
      subroutine extras_controls(id, ierr)
            integer, intent(in) :: id
            integer, intent(out) :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            
            ! this is the place to set any procedure pointers you want to change
            ! e.g., other_wind, other_mixing, other_energy  (see star_data.inc)
   
   
            ! the extras functions in this file will not be called
            ! unless you set their function pointers as done below.
            ! otherwise we use a null_ version which does nothing (except warn).
   
            s% extras_startup => extras_startup
            s% extras_start_step => extras_start_step
            s% extras_check_model => extras_check_model
            s% extras_finish_step => extras_finish_step
            s% extras_after_evolve => extras_after_evolve
            s% how_many_extra_history_columns => how_many_extra_history_columns
            s% data_for_extra_history_columns => data_for_extra_history_columns
            s% how_many_extra_profile_columns => how_many_extra_profile_columns
            s% data_for_extra_profile_columns => data_for_extra_profile_columns  
   
            s% how_many_extra_history_header_items => how_many_extra_history_header_items
            s% data_for_extra_history_header_items => data_for_extra_history_header_items
            s% how_many_extra_profile_header_items => how_many_extra_profile_header_items
            s% data_for_extra_profile_header_items => data_for_extra_profile_header_items
   
            ! my shit
            s% other_opacity_factor => other_opacity_factor
   
   
         end subroutine extras_controls
         
         
         subroutine extras_startup(id, restart, ierr)
            integer, intent(in) :: id
            logical, intent(in) :: restart
            integer, intent(out) :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
         end subroutine extras_startup
         
   
         integer function extras_start_step(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            extras_start_step = 0
         end function extras_start_step
   
   
         ! returns either keep_going, retry, or terminate.
         integer function extras_check_model(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            extras_check_model = keep_going         
            if (.false. .and. s% star_mass_h1 < 0.35d0) then
               ! stop when star hydrogen mass drops to specified level
               extras_check_model = terminate
               write(*, *) 'have reached desired hydrogen mass'
               return
            end if
   
   
            ! if you want to check multiple conditions, it can be useful
            ! to set a different termination code depending on which
            ! condition was triggered.  MESA provides 9 customizeable
            ! termination codes, named t_xtra1 .. t_xtra9.  You can
            ! customize the messages that will be printed upon exit by
            ! setting the corresponding termination_code_str value.
            ! termination_code_str(t_xtra1) = 'my termination condition'
   
            ! by default, indicate where (in the code) MESA terminated
            if (extras_check_model == terminate) s% termination_code = t_extras_check_model
         end function extras_check_model
   
   
         integer function how_many_extra_history_columns(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            how_many_extra_history_columns = 0
         end function how_many_extra_history_columns
         
         
         subroutine data_for_extra_history_columns(id, n, names, vals, ierr)
            integer, intent(in) :: id, n
            character (len=maxlen_history_column_name) :: names(n)
            real(dp) :: vals(n)
            integer, intent(out) :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            
            ! note: do NOT add the extras names to history_columns.list
            ! the history_columns.list is only for the built-in history column options.
            ! it must not include the new column names you are adding here.
            
   
         end subroutine data_for_extra_history_columns
   

         
         
         integer function how_many_extra_profile_columns(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            how_many_extra_profile_columns = 1
         end function how_many_extra_profile_columns
         
         
         subroutine data_for_extra_profile_columns(id, n, nz, names, vals, ierr)
            integer, intent(in) :: id, n, nz
            character (len=maxlen_profile_column_name) :: names(n)
            real(dp) :: vals(nz,n)
            integer, intent(out) :: ierr
            type (star_info), pointer :: s
            integer :: k
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            
            ! note: do NOT add the extra names to profile_columns.list
            ! the profile_columns.list is only for the built-in profile column options.
            ! it must not include the new column names you are adding here.
   
            ! here is an example for adding a profile column
            ! if (n /= 1) stop 'data_for_extra_profile_columns'
            
            names(1) = 'L_div_Ledd_effective'
            do k = 1, nz
               vals(k,1) = s% gradT(k) * 4.0d0 * (s % T(k) ** 4) * 7.5646d-15 / (3 * s% Peos(k))
            end do

         end subroutine data_for_extra_profile_columns
   
   
         integer function how_many_extra_history_header_items(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            how_many_extra_history_header_items = 0
         end function how_many_extra_history_header_items
   
   
         subroutine data_for_extra_history_header_items(id, n, names, vals, ierr)
            integer, intent(in) :: id, n
            character (len=maxlen_history_column_name) :: names(n)
            real(dp) :: vals(n)
            type(star_info), pointer :: s
            integer, intent(out) :: ierr
            ierr = 0
            call star_ptr(id,s,ierr)
            if(ierr/=0) return
   
            ! here is an example for adding an extra history header item
            ! also set how_many_extra_history_header_items
            ! names(1) = 'mixing_length_alpha'
            ! vals(1) = s% mixing_length_alpha
   
         end subroutine data_for_extra_history_header_items
   
   
         integer function how_many_extra_profile_header_items(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            how_many_extra_profile_header_items = 0
         end function how_many_extra_profile_header_items
   
   
         subroutine data_for_extra_profile_header_items(id, n, names, vals, ierr)
            integer, intent(in) :: id, n
            character (len=maxlen_profile_column_name) :: names(n)
            real(dp) :: vals(n)
            type(star_info), pointer :: s
            integer, intent(out) :: ierr
            ierr = 0
            call star_ptr(id,s,ierr)
            if(ierr/=0) return
   
            ! here is an example for adding an extra profile header item
            ! also set how_many_extra_profile_header_items
            ! names(1) = 'mixing_length_alpha'
            ! vals(1) = s% mixing_length_alpha
   
         end subroutine data_for_extra_profile_header_items
   
   
         ! returns either keep_going or terminate.
         ! note: cannot request retry; extras_check_model can do that.
         integer function extras_finish_step(id)
            integer, intent(in) :: id
            integer :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
            extras_finish_step = keep_going
   
            ! to save a profile, 
               ! s% need_to_save_profiles_now = .true.
            ! to update the star log,
               ! s% need_to_update_history_now = .true.
   
            ! see extras_check_model for information about custom termination codes
            ! by default, indicate where (in the code) MESA terminated
            if (extras_finish_step == terminate) s% termination_code = t_extras_finish_step
         end function extras_finish_step
         
         
         subroutine extras_after_evolve(id, ierr)
            integer, intent(in) :: id
            integer, intent(out) :: ierr
            type (star_info), pointer :: s
            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return
         end subroutine extras_after_evolve
   

!      include 'standard_run_star_extras.inc'

      end module run_star_extras
      