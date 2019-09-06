#lang rosette/safe

(provide main)

(require "stack.rkt")
(require "synthesis.rkt")

(define expr
  (+ arg0 (* 3 arg1)))

(define (main . argv)
  (define sketch (Prog 16))
  (define model
    (synthesize
      #:forall args
      #:guarantee (begin
                    (assert (= (peek (interpreter sketch)) expr)))))
  (define syms (symbolics (evaluate sketch model)))
  (define const-syms (remove* args syms same-symbol?))
  (define complete
    (complete-solution model const-syms))
  (define prog
    (evaluate sketch complete))
  (pretty-print prog))
