;+
; NAME:
;       flag_spikes
;
; PURPOSE:
;       Finds spurious spikes (single channel) in the data due to
;       feed/backend issues with GBT/VEGAS.
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
;       flag_spikes, scans, ifnums, pols, feeds, sigma, [/OUTPUT]
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
;       sigma: How many sigma above neighboring channels to flag.
;
;   threshold: Brightness above which to accept flagging. "
;
;        poly: Order of polynomial to use during baseline subtraction. "
;
; INPUT KEYWORDS:
;  /IGNORE_ENDS - Ignore the end channels. (Optional) "
;
;  /QUIET - Stop output while running. (Optional) "
;
; /SET_FLAGS - Actually set flags. (Optional)"
;
; /NO_PLOT - Do not plot spectra to files. (Optional)"
;
;
; MODIFICATION HISTORY:
;        15 Mar 2014, M.C.: Original creation date.
;-
;

pro flag_spikes, scans, ifnums, pols, feeds, sigma, threshold, poly, $
                     IGNORE_ENDS=ignore_ends, QUIET=quiet, SET_FLAGS=set_flags, NO_PLOT=no_plot
       
   no_plot = keyword_set(no_plot)
   ignore_ends = keyword_set(ignore_ends)
   quiet = keyword_set(quiet)
   set_flags = keyword_set(set_flags)
   !quiet = 1
   !EXCEPT=0

   if (n_params() lt 4) then begin
         print, "USAGE: flag_spikes, scans, ifnums, pols, feeds, sigma, threshold, poly"
         print, " scans  - GBTIDL scan numbers."
         print, " ifnums - Which ifnum= to cycle over."
         print, " pols   - Which polarizations (plnum=) to include."
         print, " feeds  - Which feeds (fdnum=) to cycle over. "
         print, " sigma  - How many sigma above neighboring channels to flag. "
         print, " threshold - Brightness above which to accept flagging. "
         print, " poly - Order of polynomial to use during baseline subtraction. "
         print, " /IGNORE_ENDS - Ignore the end channels. (Optional) "
         print, " /QUIET     - Stop output while running. (Optional) "
         print, " /SET_FLAGS - Actually set flags. (Optional)"
         print, " /NO_PLOT - Do not plot spectra to files. (Optional)"
         print, " EX.: flag_spikes, [8,10,12], [0,1,2,3,4,5,6,7], [0,1], [0,1,2,3,4,5,6,7], 3, 1, 6"
         retall
   endif

   n_flags = 0
   empty_val = -9999
   flags = indgen(5,500000)   ; first dimension is: ifnum, feed, scan, pol, channel
   flags[*,*] = empty_val
   
   for i=0,n_elements(ifnums)-1 do begin
      freqs = !g.s.observed_frequency[0]
      obs_freq = freqs[0]
      
      if (~quiet) then $
         print," **** Testing for spikes in IF #", i, " ****"
      for h=0,n_elements(feeds)-1 do begin
         for j=0,n_elements(scans)-1 do begin
            for k=0,n_elements(pols)-1 do begin
               clearregion
               clear
               freey
               freex
               getps, scans[j], ifnum=ifnums[i], plnum=pols[k], fdnum=feeds[h]
               chan
               nfit,poly
               baseline
               spectrum = getdata()
               y1 = -1.2*max(abs(spectrum[2:n_elements(spectrum)-2]))
               y2 = 1.2*max(abs(spectrum[2:n_elements(spectrum)-2]))
               sety, y1, y2
               rms = stddev(spectrum[1:1000])
               if (ignore_ends) then dl=1 else dl=0
               for l=dl,n_elements(spectrum)-dl-1 do begin
                  flagged      = 0
                  if (l eq 0) then begin
                     if (abs(spectrum[l])/rms gt sigma  and $
                         abs(spectrum[l]/spectrum[l+1]) gt sigma and $
                         abs(spectrum[l]) gt threshold) then $
                           flagged = 1
                  endif else begin
                     if (l eq n_elements(spectrum)-1) then begin
                        if (abs(spectrum[l])/rms gt sigma  and $
                         abs(spectrum[l]/spectrum[l-1]) gt sigma and $
                         abs(spectrum[l]) gt threshold) then $
                           flagged = 1
                     endif else begin
                        if (abs(spectrum[l])/rms gt sigma  and $
                            abs(spectrum[l]/spectrum[l-1]) gt sigma and $
                            abs(spectrum[l]/spectrum[l+1]) gt sigma and $
                            abs(spectrum[l]) gt threshold) then $
                              flagged = 1
                     endelse
                  endelse
                  
                  if (flagged) then begin
                     setmarker, l, spectrum[l]/1.25 ;;, label=strtrim(l,2)
                     n_flags++
                     available = where(flags[0,*] eq empty_val)
                     next = available[0]
                     flags[0,next] = ifnums[i]
                     flags[1,next] = feeds[h]
                     flags[2,next] = scans[j]
                     flags[3,next] = pols[k]
                     flags[4,next] = l
                     
                     if (SET_FLAGS) then begin
                        flag, scans[j], ifnum=ifnums[i], fdnum=feeds[h], plnum=pols[k], $
                              bchan=l, echan=l, idstring="feed/backend noise"
                     endif
                     
                     if (~quiet) then $
                        print," **** Flagged a channel! Total flags =",n_flags," ****"
                        print,"      rms   = ",rms
                        print,"      T/rms = ", abs(spectrum[l])/rms
                        print,"      chan  = ", l 
                        print,"      T (K) = ", abs(spectrum[l])
                  end
               endfor
               if (~no_plot) then begin
                  file_ps = "flag-plot_if" + strtrim(ifnums[i],2) + $
                                    "_fd" + strtrim(feeds[h],2)  + $
                                    "_sc" + strtrim(scans[j],2)  + $
                                    "_pl" + strtrim(pols[k],2)  + ".ps"
                  write_ps, file_ps
               endif
            endfor
         endfor
      endfor
   endfor

   ; Make a report.
   print," ************* Flagged Channels *************"
   print,"  total = ", n_flags
   print,"     IFNUM    FEED   SCAN     POL   CHAN "
   for p=0,n_flags-1 do begin
      print, flags[*,p]
   endfor
end
