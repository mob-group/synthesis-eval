#lang rosette/safe

(require "interpreter.rkt")

(require rosette/lib/match)

; Implements a basic stack machine with a small instruction set with the aim of
; trying out program synthesis using it.
; 
; Stacks are implemented as lists - the top of the stack is just the first
; element of the list.

(provide (all-defined-out))

; Look at the top of the stack but don't remove it
(define (peek stack)
  (car stack))

; Push a value onto the stack
(struct push (val) #:transparent)

; Pop the top value off the stack
(struct pop () #:transparent)

; Pop the two values from the top of the stack, then push their sum
(struct add () #:transparent)

; A small-step semantics function for stack programs. The state is a list (as
; defined above to represent a stack).
(define (step instruction state)
  (match instruction
    [(push val)   (cons val state)]
    [(pop)        (cdr state)]
    [(add)        (cons (+ (first state) (second state))
                       (cddr state))]))

(define (instr-cost instruction state)
  (match instruction
    [(push val)   (+ state 2)]
    [(pop)        (+ state 1)]
    [(add)        (+ state 1)]))

(define interpreter (make-interpreter null step))
(define cost        (make-interpreter 0 instr-cost))
