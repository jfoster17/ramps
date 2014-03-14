;+
; NAME:
;       reduce_single_obs
;
; PURPOSE:
;       Reduces, coadds, and averages scans from GBTIDL SDFITS data. 
;       Saves each line in individual files.
;
; AUTHOR:
;       Matthew Camarata
;       Boston University
;       725 Commonwealth Ave
;       Boston, MA 02215 USA
;       E-mail: camarata@bu.edu
;
; CATEGORY:
;       Spectra
;
; CALLING SEQUENCE:
;       reduce_single_obs, scans, ifnums, pols, file_prefix, file_suffixes
;
; RETURN VALUE:
;
; ARGUMENTS:
;       scans: GBTIDL scan numbers.
;
;      ifnums: Which ifnum= to cycle over.
;
;        pols: Which polarizations (plnum=) to include.
;
;       feeds: Which feeds (fdnum=) to cycle over.
;
; file_prefix: Prefix for files of individual spectra.
;
; file_suffix: Suffix for files of individual spectra.
;
; INPUT KEYWORDS:
;
; MODIFICATION HISTORY:
;        14 Mar 2014, M.C.: Original creation date.
;-
;

pro reduce_single_obs, scans, ifnums, pols, feeds, file_prefix, file_suffixes, QUIET=quiet
   
   if (n_elements(file_suffixes) eq 0) then file_suffixes = 0
   quiet = keyword_set(quiet)
   !quiet = 1
   !EXCEPT=0

   if (n_params() lt 4 and ~file_suffixes) then begin
         print, "USAGE: reduce_single_obs, scans, ifnums, pols, file_prefix, [file_suffixes]"
         print, " scans  - GBTIDL scan numbers."
         print, " ifnums - Which ifnum= to cycle over."
         print, " pols   - Which polarizations (plnum=) to include."
         print, " feeds  - Which feeds (fdnum=) to cycle over. "
         print, " file_prefix - Prefix for files of individual spectra."
         print, " file_suffix - Suffix for files of individual spectra."
         print, " /QUIET - shhhhhhh..."
         print, " EXAMPLE: reduce_single_obs, [8,10,12], [0,1,2,3,4,5,6,7], [0,1],"
         print, "   'W3_NH3_',['23.69-1','23.44','23.69-2','23.72','23.80','23.96','24.13','24.53']"
         retall
   endif

   if (n_elements(ifnums) ne n_elements(file_suffixes) and file_suffixes ne 0) then begin
      print, ' ERROR: number of file suffixes does not match number of IFs.'
      retall
   endif

   for i=0,n_elements(ifnums)-1 do begin
      freqs = !g.s.observed_frequency[0]
      obs_freq = freqs[0]
      
      if (~quiet and file_suffixes ne 0) then $
         print," **** Reducing IF #", i, " FILE=", file_prefix, file_suffixes[i], " ****"
      if (~quiet and file_suffixes eq 0) then $
         print," **** Reducing IF #", i, " FILE=", file_prefix, strtrim(obs_freq,2), " ****"
      for h=0,n_elements(feeds)-1 do begin
         for j=0,n_elements(scans)-1 do begin
            for k=0,n_elements(pols)-1 do begin
               getps, scans[j], ifnum=ifnums[i], plnum=pols[k], fdnum=feeds[h]
               accum
            endfor
         endfor
         ave
         if (~file_suffixes) then $
            filename = file_prefix[0] + strtrim(obs_freq,2) + '.fits' $
         else $
            filename = file_prefix[0] + file_suffixes[i] + '.fits'
         fileout, filename
         keep
         sclear   ; clear accumulator
      endfor
   endfor

end
