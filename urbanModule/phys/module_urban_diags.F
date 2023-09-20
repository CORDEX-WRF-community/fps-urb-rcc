MODULE module_urban_diags
! Module to compute urban diagnostics
!   Initiative from CORDEX Flagship Pilot Study Europe: URBan environments and Regional Climate 
!     Change, (CORDEX FPS URB RCC, https://ms.hereon.de/cordex_fps_urban/index.php.en)
!   L. Fita, CIMA, UBA-CONICET, IRL IFAECI CNRS/IRD, Argentina
!  

!
! Subroutines/Functions
!
! urban_diags: subroutine to compute trhe urban diagnostics


! Available diagnostics
! tasupav: Near-surface temperature urban pavements [K]
! tasuroof: Near-surface temperature urban roof [K]
! tasugreen: Near-surface temperature urban green spaces [K]
! tasublue: Near-surface temperature urban blue spaces [K]
! antropohfx: Anthropogenic urban heat flux [Jkg-2s-1]
! utsk: urban skin temperature [K]
! tskupav: Surface temperature urban pavements [K]
! tskuroof: Surface temperature urban roof [K]
! tskugreen: Surface temperature urban green spaces [K]
! tskublue: Surface temperature urban blue spaces [K]

  SUBROUTINE urban_diags(tasupav, tasuroof, tasugreen, tasublue,                                      &
                      antropohfx, utsk, tskupav, tskuroof, tskugreen, tskublue,                       &
                      dt, xtime, curr_secs2, radt,                                                    &
                      ids,ide, jds,jde, kds,kde,                                                      &
                      ims,ime, jms,jme, kms,kme,                                                      &
                      ips,ipe, jps,jpe, kps,kpe,                                                      & ! patch  dims
                      i_start,i_end,j_start,j_end,kts,kte,num_tiles,                                  &
                     )
                     
    USE module_dm, ONLY: wrf_dm_sum_real, wrf_dm_maxval
    USE module_configure 
  
    IMPLICIT NONE
    
!======================================================================
! Definitions
!-----------
!-- DT            time step (second)
!-- XTIME         forecast time
!-- curr_secs2    current time in seconds since simulation restart
!-- radt          frequency of radiative calls (minutes)
!
!-- ids           start index for i in domain
!-- ide           end index for i in domain
!-- jds           start index for j in domain
!-- jde           end index for j in domain
!-- kds           start index for k in domain
!-- kde           end index for k in domain
!-- ims           start index for i in memory
!-- ime           end index for i in memory
!-- jms           start index for j in memory
!-- jme           end index for j in memory
!-- ips           start index for i in patch
!-- ipe           end index for i in patch
!-- jps           start index for j in patch
!-- jpe           end index for j in patch
!-- kms           start index for k in memory
!-- kme           end index for k in memory
!-- i_start       start indices for i in tile
!-- i_end         end indices for i in tile
!-- j_start       start indices for j in tile
!-- j_end         end indices for j in tile
!-- kts           start index for k in tile
!-- kte           end index for k in tile
!-- num_tiles     number of tiles

!-------- INPUT vars --------


!-------- OUTPUT vars ------- [defined at registry.urbdiags] and included on Registry.EM_COMMON on auxhist12
! antropohfx: Anthropogenic urban heat flux [Jkg-2s-1]
! tasublue: Near-surface temperature urban blue spaces [K]
! tasugreen: Near-surface temperature urban green spaces [K]
! tasupav: Near-surface temperature urban pavements [K]
! tasuroof: Near-surface temperature urban roof [K]
! tskublue: Surface temperature urban blue spaces [K]
! tskugreen: Surface temperature urban green spaces [K]
! tskupav: Surface temperature urban pavements [K]
! tskuroof: Surface temperature urban roof [K]
! utsk: urban skin temperature [K]

    INTEGER,      INTENT(in)                             ::                                           &
                                            ids,ide, jds,jde, kds,kde,                                &
                                            ims,ime, jms,jme, kms,kme,                                &
                                            ips,ipe, jps,jpe, kps,kpe,                                &
                                            kts,kte,                                                  &
                                            num_tiles,                                                &
                                            num_soil_layers, n_moist


    INTEGER, DIMENSION(num_tiles), INTENT(in)            :: i_start, i_end, j_start, j_end
    REAL, INTENT(in)                                     :: DT, XTIME
    REAL, INTENT(in)                                     :: curr_secs2, radt

    REAL, DIMENSION(ims:ime,jms:jme), INTENT(out)        :: tasupav, tasuroof, tasugreen, tasublue
    REAL, DIMENSION(ims:ime,jms:jme), INTENT(out)        :: antropohfx
    REAL, DIMENSION(ims:ime,jms:jme), INTENT(out)        :: utsk, tskupav, tskuroof, tskugreen, tskublue


! LOCAL  VAR

    INTEGER                                              :: i, j, k, m, its, ite, jts, jte, ij
    INTEGER                                              :: idp, jdp, dimz, dimz1, dz1
    INTEGER                                              :: i1, i_1, j1, j_1, k2
    INTEGER, DIMENSION(num_tiles)                        :: i2, j2

    LOGICAL, EXTERNAL                                    :: wrf_dm_on_monitor
    CHARACTER(len=256)                                   :: msg
    LOGICAL                                              :: ijdbg
    INTEGER                                              :: dbg_level
    CHARACTER(len=50)                                    :: fname

    fname = 'urban_diags'


    ! Getting the overall debug level
    CALL get_wrf_debug_level( dbg_level ) 
    
    dimz = kme - kms + 1
    dimz1 = dimz + 1
    dz1 = dimz - 1

    ! For test purposes
    !$OMP PARALLEL DO   &
    !$OMP PRIVATE ( ij )
    DO ij = 1 , num_tiles
      i2(ij) = INT(0.5*(i_start(ij) + i_end(ij)))
      j2(ij) = INT(0.5*(j_start(ij) + j_end(ij)))
    END DO
    k2 = 0.5*(kms+kme)

    ! Computing diagnostics
    ijdbg = .FALSE.
    !$OMP PARALLEL DO   &
    !$OMP PRIVATE ( ij )
    DO ij = 1 , num_tiles
      DO i = i_start(ij), i_end(ij)
        DO j = j_start(ij), j_end(ij)
          IF (ij == 1 .AND. i == i2(ij) .AND. j == j2(ij)) ijdbg = .TRUE.

        ENDDO
      ENDDO
    ENDDO

    RETURN
  
  END SUBROUTINE urban_diags


END MODULE module_urban_diags
