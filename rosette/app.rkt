#lang rosette/safe

(provide main)

(require "stack.rkt")
(require "synthesis.rkt")

(define expr (+ arg0 arg1 35))
(define sketch (Prog 5))

(define (model cst)
  (synthesize
    #:forall args
    #:guarantee (begin
                  (assert (= (peek (interpreter sketch)) expr))
                  (assert (< (cost sketch) cst)))))

(define (main . argv)
  (define mod (find-min-sat model))
  (define syms (symbolics (evaluate sketch mod)))
  (define const-syms (remove* args syms same-symbol?))
  (define complete
    (complete-solution mod const-syms))
  (define prog
    (evaluate sketch complete))
  (pretty-print prog)
  (cost prog))
