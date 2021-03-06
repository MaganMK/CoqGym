(* Contribution to the Coq Library   V6.3 (July 1999)                    *)

(***************************************************************************)
(* File: axs_extensionnalite.v                                             *)
(* auteur: alex@sysal.ibp.fr                                               *)
(* date: 19/10/95                                                          *)
(***************************************************************************)
Require Export ZFbasis.

(***************************************************************************)
(* Axiome d'extensionnalite                                                *)
(***************************************************************************)
Axiom
  axs_extensionnalite :
    forall v0 v1 : E, (forall v2 : E, In v2 v0 <-> In v2 v1) -> v0 = v1.

(***************************************************************************)
(*                         Next : axs_paire.v                              *)
(***************************************************************************)