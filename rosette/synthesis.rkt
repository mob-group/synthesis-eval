#lang rosette/safe

(require "stack.rkt")

(require rosette/lib/synthax)

(provide (all-defined-out))

; Implement synthesis methods for the stack machine formulation - try to find
; programs that meet specific criteria.

; Symbolic values reserved for inputs to programs
(define-symbolic arg0 arg1 arg2 arg3 integer?)
(define args (list arg0 arg1 arg2 arg3))

; Symbolic values used for values within those programs
(define-symbolic a b c d e f g integer?)
(define consts (list a b c d e f g))

(define all-values (append args consts))

(define-synthax Arg
  ([(Arg) (choose arg0 arg1 arg2 arg3)]))

(define-synthax Constant
  ([(Constant) (choose a b c d e f g)]))

(define-synthax Value
  ([(Value) (choose (Arg) 
                    (Constant))]))

(define-synthax Instruction
  ([(Instruction)     (choose (nop)
                              (flip)
                              (pop) 
                              (add)
                              (sub)
                              (mul))]
   [(Instruction val) (choose (push val))]))

(define-synthax (Prog size)
  #:base null
  #:else (cons (choose (Instruction)
                       (Instruction (Value)))
               (Prog (- size 1))))

; A hack to work out if two symbols are actually the same symbol - would like to
; replace it with a better implementation.
(define (same-symbol? x y)
  (define eq-val (eq? x y))
  (if (false? eq-val)
      #f
      (null? (symbolics eq-val))))

(define (find-min-sat-rec acc proc)
  (if (sat? (proc acc))
      (proc acc)
      (find-min-sat-rec (+ 1 acc) proc)))

(define (find-min-sat proc)
  (find-min-sat-rec 0 proc))
