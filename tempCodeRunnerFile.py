    if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.sprite.spritecollide(Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), cell_group, False):
                    game_state = 'drawing'