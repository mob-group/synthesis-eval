#lang rosette/safe

(require rosette/lib/match)

(provide make-interpreter)

; Defines some tools for building interpreters out of small-step functions. They
; all follow the same pattern of instruction streams being folded over some
; initial state.

(define (make-interpreter initial-state step)
  (lambda (instrs)
    (foldl step initial-state instrs)))
